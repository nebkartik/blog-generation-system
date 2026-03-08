from src.states.blogstate import BlogState
from langchain_core.messages import HumanMessage
from src.states.blogstate import Blog

class BlogNode:
    def __init__(self,llm):
        self.llm = llm
    
    def title_node(self,state:BlogState):
       """
        Create the title for the blog.
        """
       if "topic" in state and state['topic'] and state['current_language']:
           prompt = """
                You're an expert BLog Title Creator. Use Markdown formatting & generate
                title for the {topic} and strictly in this language - {current_language}. This title should be creative & SEO friendly.
                """
           system_message = prompt.format(topic=state['topic'],current_language = state['current_language'])
           response = self.llm.invoke(system_message)
           return {"blog":{"title":response.content}}
       
    def content_node(self,state:BlogState):
            """
            Create the content for the blog.
            """
            if "topic" in state and state['topic']:
                prompt =""" 
                You're an expert Blog Writer. Generate a minimum 100 words blog based on this {topic} specifically.
                Use Markdown formatting as well.
                """
                system_message = prompt.format(topic = state['topic'])
                response = self.llm.invoke(system_message)
            return {"blog":{"title":state['blog']['title'],"content":response.content}}
      

        #    if "topic" in state and state['topic'] and state['current_language']:
        #     prompt =""" 
        #     You're an expert Blog Writer. Generate a minimum 100 words blog based on this {topic} specifically.
        #     and strictly in this language - {current_language}.
        #         Use Markdown formatting as well.
        #     """
        #     system_message = prompt.format(topic = state['topic'],current_language = state['current_language'])
            
    def translation(self,state:BlogState):
            """
            Translate the content for the blog.
            """
            translate_prompt = """
               You're an expert Blog Writer. Translate the blog for this content {content} and 
               in this language {language}
                Use Markdown formatting as well.
                 """
            system_msg = translate_prompt.format(content = state['blog']['content'],language = state['current_language'] )
            message = [
            HumanMessage(system_msg)
            ]
            translation_content = self.llm.with_structured_output(Blog).invoke(message)
            return {"blog":{"title":state['blog']['title'],"content":translation_content.content}}
    
    def route(self,state:BlogState):
         return{"current_language":state['current_language']}
    
    def route_decision(self,state:BlogState):
         if state['current_language'] == 'Hindi':
              return 'Hindi'
         elif state['current_language'] == 'French':
              return 'French'
         else:
              return state['current_language']