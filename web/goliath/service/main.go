package main

import (
	"crypto/subtle"
	"encoding/json"
	"fmt"
	"html/template"
	"io"
	"log"
	"net/http"
	"os"
)

type FlagServiceRequest struct {
	Password string `json:"password,omitempty"`
	BypassPassword  bool   `json:"-,omitempty"`
}

type FlagService struct {
	flagPassword string
	flag         string
}

func (fs FlagService) flagHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}

	var req FlagServiceRequest
	defer r.Body.Close()
	body, err := io.ReadAll(r.Body)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	if err := json.Unmarshal(body, &req); err != nil {
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	if req.BypassPassword || subtle.ConstantTimeCompare([]byte(req.Password), []byte(fs.flagPassword)) == 1 {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, `{"flag": "%s"}`, fs.flag)
		return
	}
	w.WriteHeader(http.StatusUnauthorized)
	w.Write([]byte(`{"error": "Invalid password"}`))
}

func (fs FlagService) flagSVGHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "image/svg+xml")
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(`<?xml version="1.0" encoding="UTF-8"?>
<svg width="120" height="80" viewBox="0 0 120 80" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="120" height="80" rx="16" fill="#e0f7fa"/>
  <!-- Flag pole -->
  <rect x="28" y="18" width="6" height="44" rx="3" fill="#8d5524"/>
  <!-- Waving flag -->
  <path d="M34 20 Q60 10 86 28 Q60 38 34 28 Z" fill="#ffb347" stroke="#e63946" stroke-width="2"/>
  <!-- Flag border -->
  <path d="M34 20 Q60 10 86 28 Q60 38 34 28 Z" fill="none" stroke="#e63946" stroke-width="2"/>
  <!-- Smiling face on flag -->
  <ellipse cx="60" cy="26" rx="7" ry="5" fill="#fff"/>
  <ellipse cx="57" cy="26" rx="1.2" ry="1.5" fill="#222"/>
  <ellipse cx="63" cy="26" rx="1.2" ry="1.5" fill="#222"/>
  <path d="M58 29 Q60 31 62 29" stroke="#e63946" stroke-width="1.2" fill="none"/>
  <!-- Text -->
  <text x="60" y="60" font-size="18" font-family="Comic Sans MS, Comic Sans, cursive" fill="#e63946" text-anchor="middle" font-weight="bold">CTF!</text>
</svg>`))
}

func (fs FlagService) landingPageHandler(w http.ResponseWriter, r *http.Request) {
	landingPage := `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quan Yang's Flag Store</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f0f0; text-align: center; }
        .container { margin: 50px auto; background: #fff; padding: 30px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); max-width: 400px; }
        img { width: 120px; margin-bottom: 20px; }
        input[type=password], button { padding: 10px; box-sizing: border-box; margin: 10px 0; width: 100%; }
        button { background: #007bff; color: #fff; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <img src="/flag.svg" alt="Flag Icon">
        <h2>Quan Yang's Flag Store</h2>
        <form id="flagForm">
            <input type="password" id="password" placeholder="Enter password" required />
            <button type="submit">Get Flag</button>
        </form>
        <div id="result"></div>
    </div>
    <script>
    document.getElementById('flagForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        const password = document.getElementById('password').value;
        const res = await fetch('/flag', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password })
        });
        const data = await res.json();
        const resultDiv = document.getElementById('result');
        if (res.ok) {
            resultDiv.innerHTML = '<b>Flag:</b> <code>'+data.flag+'</code>';
        } else {
            resultDiv.innerHTML = '<span style="color:red;">'+data.error+'</span>';
        }	
    });
    </script>
</body>
</html>`
	tmpl, err := template.New("landing").Parse(landingPage)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("Something went wrong"))
		fmt.Println(err)
		return
	}
	err = tmpl.Execute(w, nil)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("Something went wrong"))
		fmt.Println(err)
		return
	}
}

func main() {
	flagService := FlagService{
		flagPassword: os.Getenv("FLAG_PASSWORD"),
		flag:         os.Getenv("FLAG"),
	}
	http.HandleFunc("/", flagService.landingPageHandler)
	http.HandleFunc("/flag", flagService.flagHandler)
	http.HandleFunc("/flag.svg", flagService.flagSVGHandler)

	port := os.Getenv("PORT")
	if port == "" {
		port = "3335"
	}
	log.Printf("Quan Yang's Flag Store running on :%s", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
