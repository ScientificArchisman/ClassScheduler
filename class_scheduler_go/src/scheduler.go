package main

import "C"

import (
    "bufio"
    "encoding/json"
    "fmt"
    "os"
    "strings"

    "github.com/xuri/excelize/v2"
)

//export ReadDataFromTxt
func ReadDataFromTxt(filePath *C.char) *C.char {
    goFilePath := C.GoString(filePath)
    file, err := os.Open(goFilePath)
    if err != nil {
        return C.CString(fmt.Sprintf("error: %v", err))
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    var lines []string
    for scanner.Scan() {
        lines = append(lines, scanner.Text())
    }

    if err := scanner.Err(); err != nil {
        return C.CString(fmt.Sprintf("error: %v", err))
    }

    if len(lines) == 0 {
        return C.CString("error: file is empty")
    }

    headers := strings.Split(lines[0], "\t")
    var data []map[string]string

    for i, line := range lines[1:] {
        if strings.TrimSpace(line) == "" {
            continue
        }
        values := strings.Split(line, "\t")
        if len(values) != len(headers) {
            return C.CString(fmt.Sprintf("error: line %d does not match header length", i+2))
        }
        entry := make(map[string]string)
        for j, header := range headers {
            entry[header] = values[j]
        }
        data = append(data, entry)
    }

    jsonData, err := json.Marshal(data)
    if err != nil {
        return C.CString(fmt.Sprintf("error: %v", err))
    }

    return C.CString(string(jsonData))
}

//export ReadDataFromExcel
func ReadDataFromExcel(filePath *C.char) *C.char {
    goFilePath := C.GoString(filePath)
    f, err := excelize.OpenFile(goFilePath)
    if err != nil {
        return C.CString(fmt.Sprintf("error: %v", err))
    }
    defer f.Close()

    rows, err := f.GetRows(f.GetSheetName(0))
    if err != nil {
        return C.CString(fmt.Sprintf("error: %v", err))
    }

    if len(rows) == 0 {
        return C.CString("error: file is empty")
    }

    headers := rows[0]
    var data []map[string]string

    for i, row := range rows[1:] {
        if len(row) == 0 || strings.TrimSpace(strings.Join(row, "")) == "" {
            continue
        }
        if len(row) != len(headers) {
            return C.CString(fmt.Sprintf("error: line %d does not match header length", i+2))
        }
        entry := make(map[string]string)
        for j, header := range headers {
            entry[header] = row[j]
        }
        data = append(data, entry)
    }

    jsonData, err := json.Marshal(data)
    if err != nil {
        return C.CString(fmt.Sprintf("error: %v", err))
    }

    return C.CString(string(jsonData))
}

func main() {}
