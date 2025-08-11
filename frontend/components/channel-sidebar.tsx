"use client"

import styles from "./channel-sidebar.module.css"

interface Channel {
  id: string
  name: string
  type: "text" | "voice"
}

interface ChannelSidebarProps {
  channels: Channel[]
  selectedChannel: string
  onChannelSelect: (channelId: string) => void
  serverName: string
  user: { username: string; email: string }
  onLogout: () => void
}

export default function ChannelSidebar({
  channels,
  selectedChannel,
  onChannelSelect,
  serverName,
  user,
  onLogout,
}: ChannelSidebarProps) {
  const textChannels = channels.filter((c) => c.type === "text")
  const voiceChannels = channels.filter((c) => c.type === "voice")

  return (
    <div className={styles.sidebar}>
      <div className={styles.serverHeader}>
        <h2>{serverName}</h2>
        <button className={styles.dropdownButton}>▼</button>
      </div>

      <div className={styles.channelSection}>
        <div className={styles.categoryHeader}>
          <span>▼ TEXT CHANNELS</span>
          <button className={styles.addButton}>+</button>
        </div>
        {textChannels.map((channel) => (
          <div
            key={channel.id}
            className={`${styles.channel} ${selectedChannel === channel.id ? styles.active : ""}`}
            onClick={() => onChannelSelect(channel.id)}
          >
            <span className={styles.channelIcon}>#</span>
            <span className={styles.channelName}>{channel.name}</span>
          </div>
        ))}
      </div>

      {voiceChannels.length > 0 && (
        <div className={styles.channelSection}>
          <div className={styles.categoryHeader}>
            <span>▼ VOICE CHANNELS</span>
            <button className={styles.addButton}>+</button>
          </div>
          {voiceChannels.map((channel) => (
            <div key={channel.id} className={styles.channel}>
              <span className={styles.channelIcon}>🔊</span>
              <span className={styles.channelName}>{channel.name}</span>
            </div>
          ))}
        </div>
      )}

      <div className={styles.userArea}>
        <div className={styles.userInfo}>
          <div className={styles.avatar}>👤</div>
          <div className={styles.userDetails}>
            <div className={styles.username}>{user.username}</div>
            <div className={styles.userTag}>
              #
              {Math.floor(Math.random() * 9999)
                .toString()
                .padStart(4, "0")}
            </div>
          </div>
        </div>
        <div className={styles.userControls}>
          <button className={styles.controlButton}>🎤</button>
          <button className={styles.controlButton}>🎧</button>
          <button className={styles.controlButton} onClick={onLogout} title="Logout">
            🚪
          </button>
        </div>
      </div>
    </div>
  )
}
