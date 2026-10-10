package main

import (
    "fmt"
    "net/http"
    "io"
    "encoding/json/v2"
)


func dummyHandler(res http.ResponseWriter, req *http.Request) {
    script := req.PathValue("script");
    body, err := io.ReadAll(req.Body)
    if err != nil {
        fmt.Println("error recieving body", err)
        res.WriteHeader(400)
        return
    }
    if req.Header["Content-Type"] == nil {
        res.WriteHeader(400)
        return
    }
    if req.Header["Content-Type"][0] != "application/json" {
        res.WriteHeader(400)
        return
    }

    var parsed_body any
    err = json.Unmarshal(body, &parsed_body)
    if err != nil {
        fmt.Println("error recieving body", err)
        res.WriteHeader(400)
        return
    }

    res.Header().Add("Content-type", "application/json")
    fmt.Println(parsed_body)

    fmt.Printf("'%v' '%vn", req.URL.Path, script);
    res.Header().Add("Content-type", "application/json")
    fmt.Fprint(res, "{}")
}

func main () {
    api_base := "/api/v0"
    http.HandleFunc("/", dummyHandler);
    http.HandleFunc(api_base + "/", dummyHandler)
    http.HandleFunc(api_base + "/students", dummyHandler)
    http.HandleFunc(api_base + "/teacher_info", dummyHandler)
    http.HandleFunc(api_base + "/attendent", dummyHandler)
    http.HandleFunc(api_base + "/assignment/{action}", dummyHandler) // info, add, edit_score
    http.HandleFunc(api_base + "/calendar/{script}", dummyHandler)
    http.HandleFunc(api_base + "/file/{action}", dummyHandler) // info, upload, download
    http.HandleFunc(api_base + "/search/{script}", dummyHandler) // TODO: Change "script" to something else (ex. to_be_search, search_type)

    fmt.Println("Listening on 127.0.0.1:8080");
    fmt.Println(http.ListenAndServe("127.0.0.1:8080", nil))
}
