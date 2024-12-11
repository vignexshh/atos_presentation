from llama_index.llms.groq import Groq


class PresentationGenerator:
    def __init__(self, llm, topic, slide_count):
        self.llm = llm
        self.topic = topic
        self.slide_count = slide_count
        self.outline = None
        self.slides = None

    def generate_outline(self):
        """Generate a comprehensive outline for the topic"""
        outline_prompt = f"""Create a structured outline for '{self.topic}' 
        that can be divided into {self.slide_count} distinct sections. 
        Provide a hierarchical breakdown suitable for a presentation, 
        focusing on key aspects, chronological developments, 
        and significant points."""
        
         
        response = self.llm.complete(outline_prompt)
        self.outline = str(response).strip()
        return self.outline

    def divide_outline_into_slides(self):
        """Divide the outline into sections for specified number of slides"""
        divide_prompt = f"""Divide the following outline for '{self.topic}' 
        into exactly {self.slide_count} logical sections. 
        Each section should represent a distinct slide topic 
        that flows logically from the previous one.

        Outline:
        {self.outline}

        Provide the divided sections as a numbered list, 
        ensuring comprehensive coverage of the topic."""
        
        
        response = self.llm.complete(divide_prompt)
        self.slides = str(response).strip().split('\n')
        return self.slides

    def generate_slide_content(self):
        """Generate MARP-formatted slide content"""
        final_slides = []
        
        for i, slide_topic in enumerate(self.slides, 1):
            content_prompt = f"""Create MARP-formatted Markdown content for a slide about:
            '{slide_topic}'

            Formatting Requirements:
            - Use a single header (#) for the slide title
            - Use '-' for bullet points
            - Maximum 3-4 concise bullet points
            - Use mathematical notation where appropriate (e.g., $\pi$)
            - Keep content informative but extremely concise
            - Avoid full paragraphs
            - Include key insights and critical information"""
            
             
            response = self.llm.complete(content_prompt)
            slide_content = str(response).strip()
            
             
            formatted_slide = (
                f"---\n\n"
                f"# {slide_topic}\n\n"
                f"{slide_content}\n\n"
            )
            final_slides.append(formatted_slide)
        
        return final_slides

    def generate_presentation(self):
        """Orchestrate the entire presentation generation process"""
        
        marp_header = (
            "---\n"
            "marp: true\n"
            "theme: default\n"
            "size: 16:9\n"
            "paginate: true\n"
            "---\n\n"
        )
        
        
        title_slide = (
            "---\n\n"
            f"# {self.topic}\n\n"
            "## Comprehensive Overview\n\n"
        )
        
         
        self.generate_outline()
        self.divide_outline_into_slides()
        slides = self.generate_slide_content()
        
         
        full_presentation = (
            marp_header + 
            title_slide + 
            ''.join(slides)
        )
        
        return full_presentation




 
llm = Groq(model='llama-3.3-70b-versatile', api_key="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")

 
generator = PresentationGenerator(
    llm=llm, 
    topic="Basics of Quantum Computing", 
    slide_count=20
)

 
presentation = generator.generate_presentation()

 
print(presentation)