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
    
    def build_languag_graph(self):
        """
        Build Language Graph for blog generation"""
        self.blog_node = BlogNode(self.llm)

        #Defining Nodes
        self.graph.add_node("Title Node",self.blog_node.title_node)
        self.graph.add_node("Blog Node",self.blog_node.content_node)
        self.graph.add_node("Router",self.blog_node.route)
        self.graph.add_node("hindi_translation",lambda state: self.blog_node.translation({**state,"current_language":"Hindi"}))
        self.graph.add_node("french_translation",lambda state: self.blog_node.translation({**state,"current_language":"French"}))

        # Defining Edges
        self.graph.add_edge(START,"Title Node")
        self.graph.add_edge("Title Node","Blog Node")
        self.graph.add_edge("Blog Node","Router")
        self.graph.add_conditional_edges(
            "Router",
            self.blog_node.route_decision,
            {
                "Hindi":"hindi_translation",
                "French":"french_translation"
            }
        )
        self.graph.add_edge("hindi_translation",END)
        self.graph.add_edge("french_translation",END)

        return self.graph
    
    
    def set_graph_function(self,usecase):
        if usecase:
            graph = self.build_languag_graph()
        return graph.compile()