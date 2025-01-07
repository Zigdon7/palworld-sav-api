class FArchiveReader:
    @staticmethod
    def unpack_i32(buffer):
        try:
            if len(buffer) < 4:
                raise ValueError(f"Buffer too small for i32 unpack: expected 4 bytes, got {len(buffer)} bytes")
            return struct.unpack("<i", buffer)
        except struct.error as e:
            raise ValueError(f"Failed to unpack i32: {str(e)}")

    def read(self, size):
        try:
            data = self.archive.read(size)
            if len(data) < size:
                raise ValueError(f"Incomplete read: expected {size} bytes, got {len(data)} bytes")
            return data
        except Exception as e:
            raise ValueError(f"Failed to read {size} bytes from archive: {str(e)}")

    def fstring(self):
        try:
            size_buffer = self.read(4)
            size = self.unpack_i32(size_buffer)[0]
            
            if size < 0:
                return ""
            elif size == 0:
                return ""
            
            string_buffer = self.read(size)
            # Remove null terminator if present
            if string_buffer and string_buffer[-1] == 0:
                string_buffer = string_buffer[:-1]
            
            return string_buffer.decode('utf-8', errors='replace')
            
        except Exception as e:
            raise ValueError(f"Failed to read string: {str(e)}")
