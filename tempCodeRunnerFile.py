    # Call the face_recognition script and capture output
            output = subprocess.check_output(
                ['face_recognition', self.db_dir, unknown_img_path],
                text=True  # Ensures the output is a string (Python 3.7+)
            )
            name = output.split(',')[1].strip()
        except Exception as e:
            util.msg_box('Error', f'Face recognition failed: {str(e)}')
            return