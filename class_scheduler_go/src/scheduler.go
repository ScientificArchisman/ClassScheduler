package main

/*
#include <stdlib.h>
*/
import "C"

import (
    "bufio"
    "encoding/json"
    "fmt"
    "log"
    "os"
    "runtime"
    "strings"
    "sync"

    "github.com/xuri/excelize/v2"
)

var logger = log.New(os.Stdout, "INFO: ", log.Ldate|log.Ltime|log.Lshortfile)

// Parallel data processing with goroutines
func parallelProcess(files []string, processFunc func(string) ([]map[string]string, error)) ([]map[string]string, error) {
    var wg sync.WaitGroup
    results := make([]map[string]string, 0)
    resultCh := make(chan []map[string]string, len(files))
    errorCh := make(chan error, len(files))

    for _, file := range files {
        wg.Add(1)
        go func(file string) {
            defer wg.Done()
            data, err := processFunc(file)
            if err != nil {
                errorCh <- err
                return
            }
            resultCh <- data
        }(file)
    }

    wg.Wait()
    close(resultCh)
    close(errorCh)

    for result := range resultCh {
        results = append(results, result...)
    }

    if len(errorCh) > 0 {
        return nil, <-errorCh
    }

    return results, nil
}

// Exported function to read data from TXT files
//export ReadDataFromTxt
func ReadDataFromTxt(filePath *C.char) *C.char {
    goFilePath := C.GoString(filePath)
    data, err := readDataFromTxt(goFilePath)
    if err != nil {
        logger.Println("Error reading data from TXT:", err)
        return C.CString(fmt.Sprintf("error: %v", err))
    }

    jsonData, err := json.Marshal(data)
    if err != nil {
        logger.Println("Error marshalling data to JSON:", err)
        return C.CString(fmt.Sprintf("error: %v", err))
    }

    return C.CString(string(jsonData))
}

func readDataFromTxt(filePath string) ([]map[string]string, error) {
    file, err := os.Open(filePath)
    if err != nil {
        return nil, err
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    var lines []string
    for scanner.Scan() {
        lines = append(lines, scanner.Text())
    }

    if err := scanner.Err(); err != nil {
        return nil, err
    }

    if len(lines) == 0 {
        return nil, fmt.Errorf("file is empty")
    }

    headers := strings.Split(lines[0], "\t")
    var data []map[string]string

    for i, line := range lines[1:] {
        if strings.TrimSpace(line) == "" {
            continue
        }
        values := strings.Split(line, "\t")
        if len(values) != len(headers) {
            return nil, fmt.Errorf("line %d does not match header length", i+2)
        }
        entry := make(map[string]string)
        for j, header := range headers {
            entry[header] = values[j]
        }
        data = append(data, entry)
    }

    return data, nil
}

// Exported function to read data from Excel files
//export ReadDataFromExcel
func ReadDataFromExcel(filePath *C.char) *C.char {
    goFilePath := C.GoString(filePath)
    data, err := readDataFromExcel(goFilePath)
    if err != nil {
        logger.Println("Error reading data from Excel:", err)
        return C.CString(fmt.Sprintf("error: %v", err))
    }

    jsonData, err := json.Marshal(data)
    if err != nil {
        logger.Println("Error marshalling data to JSON:", err)
        return C.CString(fmt.Sprintf("error: %v", err))
    }

    return C.CString(string(jsonData))
}

func readDataFromExcel(filePath string) ([]map[string]string, error) {
    f, err := excelize.OpenFile(filePath)
    if err != nil {
        return nil, err
    }
    defer f.Close()

    rows, err := f.GetRows(f.GetSheetName(0))
    if err != nil {
        return nil, err
    }

    if len(rows) == 0 {
        return nil, fmt.Errorf("file is empty")
    }

    headers := rows[0]
    var data []map[string]string

    for i, row := range rows[1:] {
        if len(row) == 0 || strings.TrimSpace(strings.Join(row, "")) == "" {
            continue
        }
        if len(row) != len(headers) {
            return nil, fmt.Errorf("line %d does not match header length", i+2)
        }
        entry := make(map[string]string)
        for j, header := range headers {
            entry[header] = row[j]
        }
        data = append(data, entry)
    }

    return data, nil
}

func main() {
    runtime.GOMAXPROCS(runtime.NumCPU())
    logger.Println("Starting the Class Scheduler application...")

    // Example usage for parallel processing
    files := []string{"courses.txt", "instructors.txt", "rooms.txt", "students.txt"}
    data, err := parallelProcess(files, readDataFromTxt)
    if err != nil {
        log.Fatal("Error processing files:", err)
    }

    for _, entry := range data {
        fmt.Println(entry)
    }
}
