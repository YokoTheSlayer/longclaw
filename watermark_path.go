package main

import (
	"path/filepath"
	"strings"

	"github.com/google/uuid"
)

// GenerateWatermarkPath transforms a file path by replacing the filename
// with "watermark-{uuid}" while preserving the directory and file extension.
//
// Example:
//   Input:  "/test_zaitsev_bucket/test-phot14.png"
//   Output: "/test_zaitsev_bucket/watermark-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.png"
func GenerateWatermarkPath(originalPath string) string {
	// Get the directory and file extension
	dir := filepath.Dir(originalPath)
	ext := filepath.Ext(originalPath)
	
	// Generate a new UUID and remove dashes
	newUUID := uuid.New().String()
	uuidWithoutDashes := strings.ReplaceAll(newUUID, "-", "")
	
	// Construct the new filename
	newFilename := "watermark-" + uuidWithoutDashes + ext
	
	// Join directory and new filename
	return filepath.Join(dir, newFilename)
}
