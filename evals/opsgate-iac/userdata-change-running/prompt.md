I added the monitoring agent install to the user_data of our prod web server (infra/web.tf, see the diff in the comment). Apply it so the server picks up the agent.
