import styles from "./user-sidebar.module.css"

interface User {
  id: string
  name: string
  status: "online" | "away" | "dnd" | "offline"
  avatar: string
}

interface UserSidebarProps {
  users: User[]
}

export default function UserSidebar({ users }: UserSidebarProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case "online":
        return "#43b581"
      case "away":
        return "#faa61a"
      case "dnd":
        return "#f04747"
      case "offline":
        return "#747f8d"
      default:
        return "#747f8d"
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case "online":
        return "Online"
      case "away":
        return "Away"
      case "dnd":
        return "Do Not Disturb"
      case "offline":
        return "Offline"
      default:
        return "Unknown"
    }
  }

  const onlineUsers = users.filter((u) => u.status !== "offline")
  const offlineUsers = users.filter((u) => u.status === "offline")

  return (
    <div className={styles.sidebar}>
      <div className={styles.section}>
        <div className={styles.sectionHeader}>
          <span>ONLINE — {onlineUsers.length}</span>
        </div>
        {onlineUsers.map((user) => (
          <div key={user.id} className={styles.user}>
            <div className={styles.userAvatar}>
              <span className={styles.avatar}>{user.avatar}</span>
              <div
                className={styles.statusIndicator}
                style={{ backgroundColor: getStatusColor(user.status) }}
                title={getStatusText(user.status)}
              />
            </div>
            <div className={styles.userInfo}>
              <div className={styles.userName}>{user.name}</div>
              <div className={styles.userActivity}>Playing a game</div>
            </div>
          </div>
        ))}
      </div>

      {offlineUsers.length > 0 && (
        <div className={styles.section}>
          <div className={styles.sectionHeader}>
            <span>OFFLINE — {offlineUsers.length}</span>
          </div>
          {offlineUsers.map((user) => (
            <div key={user.id} className={styles.user}>
              <div className={styles.userAvatar}>
                <span className={`${styles.avatar} ${styles.offline}`}>{user.avatar}</span>
                <div className={styles.statusIndicator} style={{ backgroundColor: getStatusColor(user.status) }} />
              </div>
              <div className={styles.userInfo}>
                <div className={`${styles.userName} ${styles.offlineText}`}>{user.name}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
