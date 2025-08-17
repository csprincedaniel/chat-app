"use client"

import { useState } from "react"
import ServerSidebar from "@/components/server-sidebar"
import ChannelSidebar from "@/components/channel-sidebar"
import ChatArea from "@/components/chat-area"
import UserSidebar from "@/components/user-sidebar"
import styles from "./discord-app.module.css"

interface DiscordAppProps {
  user: { username: string; email: string }
  onLogout: () => void
}

export default function DiscordApp({ user, onLogout }: DiscordAppProps) {
  const [selectedServer, setSelectedServer] = useState("general")
  const [selectedChannel, setSelectedChannel] = useState("general")

  const servers = [
    { id: "general", name: "General", icon: "🏠" },
    { id: "gaming", name: "Gaming", icon: "🎮" },
    { id: "music", name: "Music", icon: "🎵" },
    { id: "coding", name: "Coding", icon: "💻" },
  ]

  const channels = {
    general: [
      { id: "general", name: "general", type: "text" },
      { id: "random", name: "random", type: "text" },
      { id: "voice-1", name: "General Voice", type: "voice" },
    ],
    gaming: [
      { id: "game-chat", name: "game-chat", type: "text" },
      { id: "lfg", name: "looking-for-group", type: "text" },
      { id: "voice-gaming", name: "Gaming Voice", type: "voice" },
    ],
    music: [
      { id: "music-share", name: "music-share", type: "text" },
      { id: "music-voice", name: "Music Voice", type: "voice" },
    ],
    coding: [
      { id: "help", name: "help", type: "text" },
      { id: "showcase", name: "showcase", type: "text" },
      { id: "code-review", name: "code-review", type: "text" },
    ],
  }

  const users = [
    { id: "1", name: "Alice", status: "online", avatar: "👩" },
    { id: "2", name: "Bob", status: "away", avatar: "👨" },
    { id: "3", name: "Charlie", status: "dnd", avatar: "🧑" },
    { id: "4", name: "Diana", status: "offline", avatar: "👩‍🦰" },
  ]

  return (
    <div className={styles.app}>
      <ServerSidebar servers={servers} selectedServer={selectedServer} onServerSelect={setSelectedServer} />
      <ChannelSidebar
        channels={channels[selectedServer] || []}
        selectedChannel={selectedChannel}
        onChannelSelect={setSelectedChannel}
        serverName={servers.find((s) => s.id === selectedServer)?.name || ""}
        user={user}
        onLogout={onLogout}
      />
      <ChatArea channelName={selectedChannel} serverName={selectedServer} currentUser={user} />
      <UserSidebar users={users} />
    </div>
  )
}
