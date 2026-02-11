from __future__ import annotations
from semantic_router import RouteLayer
from langchain.chains.base import Chain
from langchain.pydantic_v1 import Extra
from typing import Any, Dict, List, Optional
from langchain.callbacks.manager import CallbackManagerForChainRun

from extended_route import ExtendedRoute


class SemanticRouter(Chain):
    """Semantic Router Chain."""
    rag_chain: Chain
    router_layer: RouteLayer
    routes: Dict[str, ExtendedRoute]
    input_key: str = "query"  #: :meta private:
    output_key: str = "result"  #: :meta private:

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    @property
    def input_keys(self) -> List[str]:
        """Input keys.

        :meta private:
        """
        return [self.input_key]

    @property
    def output_keys(self) -> List[str]:
        """Output keys.

        :meta private:
        """
        _output_keys = [self.output_key]
        return _output_keys

    @classmethod
    def from_llm(
            cls,
            rag_chain: Chain = None,
            router_layer: RouteLayer = None
    ) -> SemanticRouter:
        """Initialize from LLM."""
        return cls(rag_chain=rag_chain, router_layer=router_layer,
                   routes={route.name: route for route in router_layer.routes})

    @property
    def _chain_type(self) -> str:
        """Return the chain type."""
        return "semantic router chain"

    def _call(
            self,
            inputs: Dict[str, Any],
            run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        """Run chain on input query."""
        query = inputs[self.input_key]

        # send user query to the router layer
        route_choice = self.router_layer(query)

        # check if a route as been found
        if route_choice.name:
            # execute the route llm to get a response
            response = self.routes[route_choice.name].langchain_llm.invoke(query)
        else:
            # if no route is found, use the rag chain to answer user question
            response = self.rag_chain.invoke({"query": query})['text']
        return {self.output_key: response}
