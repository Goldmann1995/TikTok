module.exports = {
  apps: [
    {
      name: "weilaishuo",      // 应用名称
      script: "npm",         // 启动命令
      args: "start",         // 启动参数
      env: {
        NODE_ENV: "production",
        PORT: 3000           // 运行端口
      },
      instances: 1,          // 实例数量
      autorestart: true,     // 自动重启
      watch: false,          // 文件监控
      max_memory_restart: '1G'  // 内存限制
    }
  ]
}