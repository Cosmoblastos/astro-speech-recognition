module.exports = {
  apps: [
    {
      name: "Listener",
      interpreter: "python3",
      script: "./Sistema.py",
    },
    {
      name: "Speaker",
      interpreter: "python3",
      script: "./Speaker.py",
    }
  ]
}
