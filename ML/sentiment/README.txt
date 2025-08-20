I wrote sentiment.py.

It was better practice to split them into different files.

So sentiment.py turned into preprocess_data.py, and train_model.py

I did not write the evaluation script.
I did not create the dataset.pkl file.

Last thing, I downloaded a large dataset (50K). My original code (sentiment.py) would have
used a lot of memory, and so the error "zsh: killed     /usr/local/bin/python3 /Users/daniel/chat-app/ML/sentiment/preprocess_data.py"
kept coming up. the computer kept ending the process

to fix this, I used "Sparse Representation". and "batch sizes". a LLM helped me with this.