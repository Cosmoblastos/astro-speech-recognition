module.exports = {
  apps: [
    {
      name: "listener",
      interpreter: "python3",
      script: "./Sistema.py",
    },
    {
      name: "speaker",
      interpreter: "python3",
      script: "./Speaker.py",
    }
  ]
}
