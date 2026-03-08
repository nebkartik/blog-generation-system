from langgraph.graph import StateGraph,START,END
from src.states.blogstate import BlogState
from src.nodes.blog_node import BlogNode

class GraphBuilder:
    def __init__(self,llm):
        self.llm = llm
        self.graph = StateGraph(BlogState)

    def build_graph(self):
        """
        Build Graph for blog generation"""
        self.blog_title = BlogNode(self.llm)

        self.graph.add_node("Title Node",self.blog_title.title_node)
        self.graph.add_node("Blog Node",self.blog_title.content_node)
        self.graph.add_edge(START,"Title Node")
        self.graph.add_edge("Title Node","Blog Node")
        self.graph.add_edge("Blog Node",END)

        return self.graph
    
    def set_graph_function(self,usecase):
        if usecase:
            graph = self.build_graph()
        return graph.compile()