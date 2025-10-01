package main

import (
	"strings"
	"testing"
)

func TestGenerateWatermarkPath(t *testing.T) {
	tests := []struct {
		name       string
		input      string
		wantPrefix string
		wantExt    string
	}{
		{
			name:       "PNG file",
			input:      "/test_zaitsev_bucket/test-phot14.png",
			wantPrefix: "/test_zaitsev_bucket/watermark-",
			wantExt:    ".png",
		},
		{
			name:       "JPG file",
			input:      "/test_zaitsev_bucket/photo.jpg",
			wantPrefix: "/test_zaitsev_bucket/watermark-",
			wantExt:    ".jpg",
		},
		{
			name:       "JPEG file",
			input:      "/test_zaitsev_bucket/image.jpeg",
			wantPrefix: "/test_zaitsev_bucket/watermark-",
			wantExt:    ".jpeg",
		},
		{
			name:       "HEIC file",
			input:      "/test_zaitsev_bucket/file.heic",
			wantPrefix: "/test_zaitsev_bucket/watermark-",
			wantExt:    ".heic",
		},
		{
			name:       "AVIF file",
			input:      "/test_zaitsev_bucket/test.avif",
			wantPrefix: "/test_zaitsev_bucket/watermark-",
			wantExt:    ".avif",
		},
		{
			name:       "Nested path",
			input:      "/bucket/subfolder/image.png",
			wantPrefix: "/bucket/subfolder/watermark-",
			wantExt:    ".png",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := GenerateWatermarkPath(tt.input)

			// Check that result starts with expected prefix
			if !strings.HasPrefix(result, tt.wantPrefix) {
				t.Errorf("GenerateWatermarkPath() = %v, want prefix %v", result, tt.wantPrefix)
			}

			// Check that result ends with expected extension
			if !strings.HasSuffix(result, tt.wantExt) {
				t.Errorf("GenerateWatermarkPath() = %v, want extension %v", result, tt.wantExt)
			}

			// Check that UUID part doesn't contain dashes
			// Extract the part between "watermark-" and extension
			uuidPart := strings.TrimPrefix(result, tt.wantPrefix)
			uuidPart = strings.TrimSuffix(uuidPart, tt.wantExt)
			
			if strings.Contains(uuidPart, "-") {
				t.Errorf("UUID part contains dashes: %v", uuidPart)
			}

			// Check UUID length (32 characters without dashes)
			if len(uuidPart) != 32 {
				t.Errorf("UUID part length = %v, want 32", len(uuidPart))
			}
		})
	}
}
