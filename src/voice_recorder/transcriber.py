import whisper

class AudioTranscriber:
    def __init__(self, model_name="base.en"):
        """
        Initialize the transcriber with a Whisper model.
        
        Args:
            model_name (str): Whisper model name to use (e.g., "base.en", "small.en", "medium.en")
        """
        self.model = whisper.load_model(model_name)
        
    def transcribe(self, audio_np):
        """
        Transcribe audio data to text.
        
        Args:
            audio_np (numpy.ndarray): Audio data as a numpy array
            
        Returns:
            str: Transcribed text
        """
        if audio_np is None or audio_np.size == 0:
            return "No audio recorded"
            
        result = self.model.transcribe(audio_np, fp16=False)
        return result["text"].strip()
