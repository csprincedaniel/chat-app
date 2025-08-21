from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from typing import List, Tuple, Optional, Dict

import re
from datetime import datetime, timedelta
import json


class SummaryBot:

    def __init__(self, model_name: str = "facebook/bart-large-cnn"):

        print(f"Loading summarization model: {model_name}")

        try: 
            self.summarizer = pipeline(
                "summarization", 
                model=model_name,
                tokenizer=model_name,
                device = 0 if torch.cuda.is_available() else -1
            )

            self.model_name = model_name

            print(f"Model successfully loaded")

        except Exception as e:
            print(f"Loading model failed with {e} error")

            print(f"Falling back to distilbart model")

            self.summarizer = pipeline(
                "summarization",
                model="sshleifer/distilbart-cnn-12-6",
                device = -1 # Using CPU for smaller model.
            )

            self.model_name = "sshleifer/distilbart-cnn-12-6"


    def preprocess_messages(self, messages: List[dict]) -> str:

        # Checks if a message is there in the first place.
        if not messages: 
            return

        # Sorting the messages based off of timestamp of the messages
        sorted_messages = sorted(messages, key=lambda x: x.get('timestamp', ''))

        formatted_message = ''

        for msg in messages:
            content = msg.get('content', '').strip()
            user_id = msg.get('user_id', 'Unknown')

            if len(content) < 3:
                continue

            # Removing mentions, URLS and discord formatting from the message.
            content = self.clean_message_content(content)

            # If there is any text left after cleaning then add it to the formatted text.
            if content:
                formatted_message += f"{user_id}: {content}\n"


        return formatted_message


    def clean_messages_content(self, content: str) -> str:

        # re.sub is for substitue
        # r'@' checks if a word starts with @ and \w+ includes the rest of the letters
        # in a stingle string that starts with @ and replaces it with '' so deletes it.
        # If you used /w instead of /w+ this would only delete the first letter that follows 
        # @ so for example @John -> ohn when it should be fully deleted.
        content = re.sub(r'@\w+', '', content)


        # Removing channel mentions
        # Using [\w-]+ instead of \w+
        # because for channel mentions like 
        # #cat-memes using \w+  ->  -memes
        # while using [\w-]+  ->  ''
        content = re.sub(r'#[\w-]+', '', content)


        # Removing URL's from the content of the message
        content = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', content)

        # Removing extra white space from message
        content = re.sub(r'\s+', '', content)


        # Removing emojis

        content = re.sub(r'<:\w+:\d+>', '', content)


    # Splits long text into smaller ones for easier processing
    def chunk_text(self, text:str, max_chunk_size: int = 1000):

        if len(text) <= max_chunk_size:
            return [text]

        chunks = []

        # Split by user messages a user message ends with a \n
        sentences = text.split('\n')

        current_chunk = ""

        for sentence in sentences:

            if len(current_chunk + sentence) <= max_chunk_size:
                current_chunk += sentence + '\n'

            # If adding next sentence overflows the max chunk size,
            # append the current chunk and replace the current chunk
            # with the next sentence.
            else:

                if current_chunk:
                    chunks.append(current_chunk.strip())


                current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks


    def generate_summary(self, text: str, max_length: int = 150, min_length: int = 30) -> str:

        if not text or len(text.strip()) < 50:
            return "Not enough text to summarize."

        try:

            # If the text is too long, slice it into smaller chunks of text.
            chunks = self.chunk_text(text=text, max_chunk_size=1000)

            # If the text isn't sliced then summarize it normally.
            if len(chunks) == 1:

                # self.summarizer calls the hugging face pipeline
                # which returns a map that looks like

                # {"summary_text": "The summary of the text"}

                # [0]['summary_text'] grabs the first element in the map
                summary = self.summarizer(
                    text, 
                    max_length=max_length,
                    min_length=min_length,

                    # If set do_sample=True the 
                    # results of the summary will vary like how chatgpt
                    # has different responses to same prompt.

                    do_sample=False, # Using greedy decoding for consistency

                    # If text is too long then cut it off, wihtout truncation=True
                    # summarization would crash with text too long.
                    truncation=True
                )[0]['summary_text']


            # If there are multiple chunks of text, summarize each of them 
            # then combine.
            else:

                chunk_summaries = []

                for chunk in chunks:

                    chunk_summary = self.summarizer(
                        chunk,
                        max_length=100,
                        min_length=20,
                        do_sample=False,
                        truncation=True
                    )[0]['summary_text']

                    chunk_summaries.append(chunk_summary)

                combined_chunks = " ".join(chunk_summaries)

                # If the length of the summarized chunks is too long,
                # summarize again.
                if len(combined_chunks) > 500:
                    summary = self.summarizer(
                        combined_chunks,
                        max_length=max_length,
                        min_length=min_length,
                        do_sample=False,
                        truncation=True
                    )[0]['summary_text']

                else:
                    summary = combined_chunks



            return summary

        except Exception as e:
            print(f"Error generating summary: {e}")

            return "Sorry couldn't summarize"


    def summarize_channel_messages(self, messages: List[Dict], 
                                time_window_hours: Optional[int] = None) -> Dict:

        # Checks if there are any messages in the first place.
        if not messages:
            return {
                "summary": "None",
                "message_count": 0,
                "time_range": None,
                "generated_at": datetime.now().isoformat()
            }


        # Filter messages by time window

        if time_window_hours:
            cutoff_time = datetime.now() - timedelta(hours=time_window_hours)

            messages = [
                msg for msg in messages 
                if datetime.fromisoformat(msg.get('timestamp','')) > cutoff_time
            ]


        # checks if there are any messages within the timeframe.
        if not messages:

            return {
                "summary": f"No messages found in the last {time_window_hours} hour",
                "message_count": 0,
                "time_range": None,
                "generated_at": datetime.now().isoformat()
            }


        formatted_text = self.preprocess_messages(messages)

        if not formatted_text:
            return {
                "summary": "No meaningful content found to summarize.",
                "message_count": len(messages),
                "time_range": None,
                "generated_at": datetime.now().isoformat()
            }


        summary = self.generate_summary(formatted_text) 

        timestamps = [msg.get('timestamp') for msg in messages if msg.get('timestamp')]

        time_range = None

        if timestamps:

            time_range = {
                "start": min(timestamps),
                "end": max(timestamps)
            }

        return {
            "summary": summary,
            "message_count": len(messages),
            "time_range": time_range,
            "generated_at": datetime.now().isoformat(),
            "model_used": self.model_name
        }

    