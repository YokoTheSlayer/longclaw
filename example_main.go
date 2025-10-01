package main

import "fmt"

func main() {
	// Example usage
	originalPath := "/test_zaitsev_bucket/test-phot14.png"
	watermarkPath := GenerateWatermarkPath(originalPath)
	
	fmt.Printf("Original path:  %s\n", originalPath)
	fmt.Printf("Watermark path: %s\n", watermarkPath)
	
	// More examples with different file types
	examples := []string{
		"/test_zaitsev_bucket/photo.jpg",
		"/test_zaitsev_bucket/image.jpeg",
		"/test_zaitsev_bucket/file.heic",
		"/test_zaitsev_bucket/test.avif",
	}
	
	fmt.Println("\nДополнительные примеры:")
	for _, path := range examples {
		fmt.Printf("%s -> %s\n", path, GenerateWatermarkPath(path))
	}
}
