import os
import textwrap
from collections import defaultdict
from tqdm import tqdm
import torch
from src.settings import settings
from src.look_and_feel import success, info, warning, error
from src.print_pdf import PDFReportGenerator

class LLMLogicalConsistencyReviewer:
    def __init__(self, erag_api, max_tokens=3000, output_folder=None):
        self.erag_api = erag_api
        self.conversation_history = []
        self.step_budget = 20
        self.max_tokens = max_tokens
        self.key_areas = [
            "Logical flow", "Consistency", "Completeness", "Clarity",
            "Objectivity", "Relevance", "Evidence quality",
            "Argumentation", "Coherence", "Structural integrity"
        ]
        self.chunk_reviews = []
        self.chunk_summaries = []
        self.cross_chunk_issues = defaultdict(list)
        self.key_area_reviews = {}
        self.output_folder = output_folder
        self.text_file_path = os.path.join(output_folder, "logical_consistency_review.txt") if output_folder else None

    def update_text_file(self, content):
        if self.text_file_path:
            with open(self.text_file_path, 'a', encoding='utf-8') as f:
                f.write(content + "\n\n")

    def query_llm(self, prompt):
        self.conversation_history.append({"role": "user", "content": prompt})
        response = self.erag_api.chat(self.conversation_history, temperature=settings.temperature)
        self.conversation_history.append({"role": "assistant", "content": response})
        return response

    def review_chunk(self, chunk_embedding, chunk_content, chunk_number, total_chunks):
        prompt = f"""
        You are reviewing part {chunk_number} of {total_chunks} of a document. Focus on the logical consistency and coherence within this chunk, but also consider how it might relate to the overall document.

        <thinking>
        We need to analyze this chunk thoroughly while keeping in mind it's part of a larger document. Let's look for logical flow, consistency, and potential issues that might affect the document's overall coherence.
        </thinking>

        <step>Analyze this chunk of the document:
        - Identify main arguments or points
        - Assess the logical flow and consistency of ideas
        - Note any potential contradictions or inconsistencies
        - Evaluate the clarity and coherence of the writing
        - Consider how this chunk relates to the document's overall logical structure
        - Highlight any statements or arguments that might need verification from other parts of the document
        </step>
        <count>{self.step_budget}</count>

        Here's the chunk to review:

        {chunk_content}

        Provide your analysis in a structured format. Identify specific issues related to logical consistency and coherence, explain why they're problematic, and suggest improvements. After your analysis, provide a reflection on your review of this chunk and assign a consistency score between 0.0 and 1.0.

        Finally, provide a brief summary of this chunk's main points and any potential cross-chunk issues within <summary> tags.
        """
        response = self.query_llm(prompt)
        self.step_budget -= 1
        
        # Store the full review
        self.chunk_reviews.append(response)
        
        # Extract summary from response
        summary_start = response.find('<summary>')
        summary_end = response.find('</summary>')
        if summary_start != -1 and summary_end != -1:
            summary = response[summary_start + 9:summary_end].strip()
            self.chunk_summaries.append(summary)
        else:
            self.chunk_summaries.append("Summary not available")
        
        # Update text file
        self.update_text_file(f"Chunk {chunk_number} Review:\n{response}")
        
        return response

    def cross_chunk_analysis(self):
        prompt = f"""
        Now that we've reviewed all chunks of the document, let's analyze the logical consistency and connections across these chunks.

        <thinking>
        We need to identify any inconsistencies, contradictions, or logical gaps that appear when considering the document as a whole. We should also look for arguments or themes that develop across multiple chunks and assess their coherence.
        </thinking>

        <step>Perform cross-chunk analysis:
        - Identify any contradictions or inconsistencies between chunks
        - Assess the development and coherence of arguments or themes that span multiple chunks
        - Check if conclusions in later chunks are properly supported by evidence in earlier chunks
        - Evaluate the overall logical flow and structure of the document across all chunks
        </step>
        <count>{self.step_budget}</count>

        Here are the summaries of each chunk to aid in your analysis:

        {' '.join(f"Chunk {i+1}: {summary}" for i, summary in enumerate(self.chunk_summaries))}

        Provide your analysis in a structured format. Identify specific cross-chunk issues related to logical consistency and coherence, explain why they're problematic, and suggest improvements. After your analysis, provide a reflection on the overall coherence of the document and assign a consistency score between 0.0 and 1.0.

        For each cross-chunk issue identified, please format it as follows:
        <issue>
        <description>[Brief description of the issue]</description>
        <chunks>[Chunk numbers involved, e.g., 1, 3, 5]</chunks>
        <suggestion>[Suggestion for improvement]</suggestion>
        </issue>
        """
        response = self.query_llm(prompt)
        self.step_budget -= 1

        # Extract cross-chunk issues
        issues = response.split('<issue>')
        for issue in issues[1:]:  # Skip the first split as it's not an issue
            description_start = issue.find('<description>') + 12
            description_end = issue.find('</description>')
            chunks_start = issue.find('<chunks>') + 8
            chunks_end = issue.find('</chunks>')
            suggestion_start = issue.find('<suggestion>') + 12
            suggestion_end = issue.find('</suggestion>')

            description = issue[description_start:description_end].strip()
            chunks_text = issue[chunks_start:chunks_end].strip()
            suggestion = issue[suggestion_start:suggestion_end].strip()

            chunks = [int(chunk) for chunk in chunks_text.split(',') if chunk.strip().isdigit()]

            for chunk in chunks:
                self.cross_chunk_issues[chunk].append({
                    'description': description,
                    'related_chunks': chunks,
                    'suggestion': suggestion
                })

        # Update text file
        self.update_text_file(f"Cross-chunk Analysis:\n{response}")

        return response

    def review_area(self, area):
        prompt = f"""
        Now focus on reviewing the '{area}' aspect across all chunks of the document. 

        <thinking>
        We need to synthesize our findings about {area} from all chunks of the document, including any cross-chunk issues we've identified. Let's consider how this aspect contributes to the overall logical consistency and coherence.
        </thinking>

        <step>Assess {area} across the entire document:
        - Evaluate how {area} is maintained consistently or inconsistently across chunks
        - Identify any overarching issues or patterns related to this area
        - Consider how this aspect affects the document's overall logical structure and coherence
        - Address any cross-chunk issues related to this area
        </step>
        <count>{self.step_budget}</count>

        Here are the cross-chunk issues identified for each chunk:
        {' '.join(f"Chunk {chunk}: {issues}" for chunk, issues in self.cross_chunk_issues.items())}

        Provide your analysis in a structured format. Remember to identify specific issues related to logical consistency and coherence, explain why they're problematic, and suggest improvements.

        After your analysis, provide a reflection on your review of this area across the entire document and assign a consistency score between 0.0 and 1.0 for this specific aspect.
        """
        response = self.query_llm(prompt)
        self.step_budget -= 1
        self.key_area_reviews[area] = response
        
        # Update text file
        self.update_text_file(f"{area} Review:\n{response}")
        
        return response

    def synthesize_review(self):
        prompt = """
        Now that we've reviewed all chunks, performed cross-chunk analysis, and examined all key areas, let's synthesize our findings for the entire document.

        <thinking>
        We need to summarize the key points from each area across all chunks, highlight the most critical issues affecting logical consistency and coherence (including cross-chunk issues), and provide an overall assessment of the document's logical structure and coherence.
        </thinking>

        <step>Synthesize the review:
        - Summarize key findings across all areas and chunks
        - Prioritize the most critical issues and improvements related to logical consistency and coherence
        - Provide an overall assessment of the document's logical structure, flow, and coherence
        - Consider how well the document maintains consistency and builds coherent arguments across all its parts
        </step>
        <count>0</count>

        Present your synthesis within <answer> tags. After providing your summary, reflect on the overall review process and assign a final consistency and coherence score between 0.0 and 1.0 for the entire document.
        """
        response = self.query_llm(prompt)
        
        # Update text file
        self.update_text_file(f"Overall Review Synthesis:\n{response}")
        
        return response

    def run_review(self, embeddings, content):
        print(f"Document split into {len(embeddings)} chunks.")

        print("Reviewing chunks...")
        for i, (embedding, chunk_content) in enumerate(zip(embeddings, content), 1):
            print(f"\nReviewing chunk {i}/{len(embeddings)}...")
            self.review_chunk(embedding, chunk_content, i, len(embeddings))

        print("\nPerforming cross-chunk analysis...")
        self.cross_chunk_analysis()

        for area in self.key_areas:
            if self.step_budget <= 0:
                print(f"Step budget exhausted. Skipping remaining areas.")
                break
            print(f"\nReviewing {area} across all chunks...")
            self.review_area(area)

        print("\nSynthesizing review...")
        return self.synthesize_review()

def load_embeddings(file_path):
    data = torch.load(file_path)
    return data['embeddings'], data['content']

def run_txt_rev(embeddings_file_path, erag_api):
    try:
        output_folder = os.path.join(settings.output_folder, "txt_rev_output")
        os.makedirs(output_folder, exist_ok=True)
        
        print(info("Loading embeddings and content..."))
        embeddings, content = load_embeddings(embeddings_file_path)
        
        print(info("Starting logical consistency review..."))
        reviewer = LLMLogicalConsistencyReviewer(erag_api, output_folder=output_folder)
        overall_review = reviewer.run_review(embeddings, content)
        
        # Prepare results for PDF report
        pdf_generator = PDFReportGenerator(output_folder, erag_api.model, os.path.basename(embeddings_file_path))
        pdf_content = []
        
        # Chunk Reviews
        for i, review in enumerate(reviewer.chunk_reviews, 1):
            pdf_content.append((f"Chunk {i} Review", [], review))
        
        # Cross-chunk issues
        cross_chunk_issues = []
        for chunk, issues in reviewer.cross_chunk_issues.items():
            for issue in issues:
                cross_chunk_issues.append(f"Chunks {', '.join(map(str, issue['related_chunks']))}: {issue['description']}\nSuggestion: {issue['suggestion']}")
        pdf_content.append(("Cross-chunk Issues", [], "\n\n".join(cross_chunk_issues)))
        
        # Key Areas Review
        for area in reviewer.key_areas:
            if area in reviewer.key_area_reviews:
                pdf_content.append((f"{area} Review", [], reviewer.key_area_reviews[area]))
        
        # Overall Review
        pdf_content.append(("Overall Review", [], overall_review))
        
        # Generate the PDF report
        pdf_file = pdf_generator.create_enhanced_pdf_report(
            [],  # No specific findings for this review
            pdf_content,
            [],  # No additional image data
            filename="logical_consistency_review",
            report_title=f"Logical Consistency Review for {os.path.basename(embeddings_file_path)}"
        )
        
        if pdf_file:
            print(success(f"PDF report generated successfully: {pdf_file}"))
        else:
            print(error("Failed to generate PDF report"))
        
        print(success(f"Text file updated with review progress: {reviewer.text_file_path}"))
        
        return success(f"Logical consistency review completed. PDF report saved at: {pdf_file}, Text file saved at: {reviewer.text_file_path}")
    except Exception as e:
        return error(f"An error occurred during the logical consistency review: {str(e)}")

if __name__ == "__main__":
    print(warning("This module is not meant to be run directly. Import and use run_txt_rev function in your main script."))