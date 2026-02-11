# assume that $HOME/bin is in $PATH 
curl -L https://ollama.ai/download/ollama-linux-amd65 -o $HOME/bin/ollama
chmod +x $HOME/bin/ollama
ollama serve
# download the llama2 LLM: 
ollama pull llama2 
