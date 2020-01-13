package main

import "fmt"

func intSeq() func() int { // function intSeq() returns a function of int
	i := 0
	return func() int {
		i++
		return i
	}
}

func main() {
	nextInt := intSeq() // Assign the function to a variable in main

	fmt.Println(nextInt())
	fmt.Println(nextInt())
	fmt.Println(nextInt())

	newInts := intSeq()
	fmt.Println(newInts())
}
