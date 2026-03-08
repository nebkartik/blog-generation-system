from src.states.blogstate import BlogState

class BlogNode:
    def __init__(self,llm):
        self.llm = llm
    
    def title_node(self,state:BlogState):
       """
        Create the title for the blog.
        """
       if "topic" in state and state['topic']:
           prompt = """
                You're an expert BLog Title Creator. Use Markdown formatting & generate
                title for the {topic}. This title should be creative & SEO friendly.
                """
           system_message = prompt.format(topic=state['topic'])
           response = self.llm.invoke(system_message)
           return {"blog":{"title":response.content}}
       
    def content_node(self,state:BlogState):
           if "topic" in state and state['topic']:
            prompt =""" 
            You're an expert Blog Writer. Generate a minimum 100 words blog based on this {topic} specifically.
                Use Markdown formatting as well.
            """
            system_message = prompt.format(topic = state['topic'])
            response = self.llm.invoke(system_message)
            return {"blog":{"title":state['blog']['title'],"content":response.content}}