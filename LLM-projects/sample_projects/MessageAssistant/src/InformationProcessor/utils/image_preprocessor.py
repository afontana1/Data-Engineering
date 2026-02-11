import os
import io
import requests
import base64
import numpy as np
from scipy.fftpack import dct
from PIL import Image


class ImageHasher:
    @staticmethod
    def hex_collector(bits):
        hex_strings = []
        for i in range(0, len(bits), 4):
            decimal = int(bits[i:i + 4], 2)
            hex_strings.append(hex(decimal)[2:].rjust(1, '0'))
        return hex_strings

    def average_hash(self, image_data):
        """
        Generate an average hash for the image (aHash).
        """
        image = Image.open(io.BytesIO(image_data))
        image = image.convert('L').resize((8, 8), Image.LANCZOS)

        pixels = list(image.getdata())
        avg = sum(pixels) / len(pixels)
        bits = ''.join(['1' if (pixel >= avg) else '0' for pixel in pixels])

        # Convert bits to hexadecimal
        hex_string = self.hex_collector(bits)

        return ''.join(hex_string)

    def perceptual_hash(self, image_data):
        """
        Generate a perceptual hash for an image (pHash).
        """
        image = Image.open(io.BytesIO(image_data))
        image = image.convert('L').resize((32, 32), Image.LANCZOS)

        pixels = np.array(image.getdata(), dtype=np.cfloat).reshape((32, 32))
        dct_value = dct(dct(pixels, axis=0), axis=1)
        dct_low_freq = dct_value[:8, :8]

        median_value = np.median(dct_low_freq)
        bits = ''.join(['1' if pixel > median_value else '0' for pixel in dct_low_freq.flatten()])

        # Convert bits to hexadecimal
        hex_string = self.hex_collector(bits)

        return ''.join(hex_string)

    @staticmethod
    def difference_hash_image(image_data):
        """
        Generate a hash for an image using the dHash algorithm.
        """
        image = Image.open(io.BytesIO(image_data))
        image = image.convert('L').resize((9, 8), Image.LANCZOS)

        # Compare adjacent pixels.
        difference = []
        for row in range(8):
            for col in range(8):
                pixel_left = image.getpixel((col, row))
                pixel_right = image.getpixel((col + 1, row))
                difference.append(pixel_left > pixel_right)

        # Convert the binary array to a hexadecimal string.
        decimal_value = 0
        hex_string = []
        for index, value in enumerate(difference):
            if value:  # If this pixel is more intense than the next one
                decimal_value += 2 ** (index % 8)
            if (index % 8) == 7:  # Every 8 bits, append hex character
                hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
                decimal_value = 0

        return ''.join(hex_string)

    def combined_hash(self, image_data):
        """
        Combine dHash, aHash, and pHash to generate a more robust hash.
        """
        return self.difference_hash_image(image_data) + self.average_hash(image_data) + self.perceptual_hash(image_data)


class ImageDescriber:
    def __init__(self, api_key):
        self.api_key = api_key

    @staticmethod
    def encode_image(image_path):
        """
        Encode the image to a base64 string.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    @staticmethod
    def get_image_metadata(image_path):
        """
        Get metadata of the image file.
        """
        metadata = {}
        try:
            metadata['size'] = os.path.getsize(image_path)
            metadata['modified_time'] = os.path.getmtime(image_path)
            metadata['created_time'] = os.path.getctime(image_path)
        except OSError as e:
            print(f"Error retrieving metadata: {e}")
        return metadata

    def describe_image(self, image_path):
        """
        Send a request to OpenAI to get the description of the image.
        """
        base64_image = self.encode_image(image_path)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What’s in this image?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 500
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        description = response.json()['choices'][0]['message']['content']
        return description
