package main

import (
    "fmt"
    "net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hi, my name is %s", r.URL.Path[1:])
}

func main() {
    http.HandleFunc("/", handler)
    fmt.Printf("Now serving on 8080...")
    http.ListenAndServe(":8080", nil)
}