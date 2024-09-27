from youtube_transcript_api import YouTubeTranscriptApi


def get_transcript_of_yt_video(v_id):

    try:

        transcript_list = YouTubeTranscriptApi.list_transcripts(v_id)
        l = len(list(transcript_list))

        if (l > 1):
            try:
                final_transcript = YouTubeTranscriptApi.get_transcript(
                    v_id, languages=['en'])
                return final_transcript
            except:
                for i in transcript_list:
                    start_with = str(i)[:2]
                    transcript = transcript_list.find_transcript([start_with])
                    final_transcript = transcript.translate('en').fetch()
                    return final_transcript
        else:
            for i in transcript_list:
                start_with = str(i)[:2]
                if start_with == 'en':
                    final_transcript = YouTubeTranscriptApi.get_transcript(
                        v_id, languages=['en'])
                else:
                    transcript = transcript_list.find_transcript([start_with])
                    final_transcript = transcript.translate('en').fetch()
                return final_transcript

    except:

        final_transcript = "0"
        return final_transcript
