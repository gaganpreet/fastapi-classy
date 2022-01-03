from typing import Any, Dict, Sequence, get_type_hints
from fastapi import APIRouter, params


class FastAPIClassy:
    class Meta:
        tags: Sequence[str] = []
        dependencies: Sequence[params.Depends] = []

    @classmethod
    def make_router(cls) -> APIRouter:
        router = APIRouter()
        method_names = set(
            fn_name
            for fn_name in dir(cls)
            if callable(getattr(cls, fn_name)) and fn_name[0] != "_"
        )
        method_names = method_names - set(("make_router", "Meta"))

        kwargs: Dict[str, Any] = {}
        if hasattr(cls.Meta, "dependencies"):
            kwargs["dependencies"] = cls.Meta.dependencies
        if hasattr(cls.Meta, "tags"):
            kwargs["tags"] = cls.Meta.tags

        for method_name in method_names:
            method = getattr(cls, method_name)
            return_type = get_type_hints(method).get("return")
            if return_type:
                kwargs = {**kwargs, "response_model": return_type}
            if method_name == "get":
                router.add_api_route("/{id}", method, methods=["GET"], **kwargs)
            elif method_name == "index":
                router.add_api_route("/", method, methods=["GET"], **kwargs)
            elif method_name == "delete":
                router.add_api_route("/{id}", method, methods=["DELETE"], **kwargs)
            elif method_name == "patch":
                router.add_api_route("/{id}", method, methods=["PATCH"], **kwargs)
            elif method_name == "put":
                router.add_api_route("/{id}", method, methods=["PUT"], **kwargs)
            elif method_name == "post":
                router.add_api_route("/{id}", method, methods=["POST"], **kwargs)
            else:
                router.add_api_route(f"/{method_name}", method)
        return router
