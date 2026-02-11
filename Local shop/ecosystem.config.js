module.exports = {
  apps: [
    {
      name: "local-shop",
      script: "main.py",
      interpreter: "python", // Ensure 'python' is in your system PATH
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "1G",
      time: true,
      env: {
        NODE_ENV: "production",
        PORT: 5000,
        PYTHONIOENCODING: "utf-8",
        // Add your production secrets here or in the system environment
        // MONGO_DETAILS: "mongodb+srv://...",
        // SECRET_KEY: "..."
      },
    },
    // Optional: Public URL Tunnel (Like Ngrok)
    // Uncomment the block below to get a public URL automatically
    // {
    //   name: "tunnel",
    //   script: "npx",
    //   args: "localtunnel --port 5000",
    //   autorestart: true
    // }
  ],
};