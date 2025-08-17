"use client"

import styles from "./server-sidebar.module.css"

interface Server {
  id: string
  name: string
  icon: string
}

interface ServerSidebarProps {
  servers: Server[]
  selectedServer: string
  onServerSelect: (serverId: string) => void
}

export default function ServerSidebar({ servers, selectedServer, onServerSelect }: ServerSidebarProps) {
  return (
    <div className={styles.sidebar}>
      <div className={styles.serverList}>
        {servers.map((server) => (
          <div
            key={server.id}
            className={`${styles.serverIcon} ${selectedServer === server.id ? styles.active : ""}`}
            onClick={() => onServerSelect(server.id)}
            title={server.name}
          >
            <span className={styles.icon}>{server.icon}</span>
          </div>
        ))}
        <div className={styles.addServer}>
          <span>+</span>
        </div>
      </div>
    </div>
  )
}
