from ..config.llm_config import ConfigGPT, ConfigLLM


class FastappSettings:
    extra_reponse_system_prompts: list[str] = []
    extra_selection_system_prompts: list[str] = []
    len_context: int = ConfigLLM.DEFAULT_HISTORY_LEN
    
    def update(
        extra_reponse_system_prompts: list[str] | None = None,
        extra_selection_system_prompts: list[str] | None = None,
        len_context: int | None = None,
    ):
        if extra_reponse_system_prompts is not None:
            FastappSettings.extra_reponse_system_prompts = extra_reponse_system_prompts
        if extra_selection_system_prompts is not None:
            FastappSettings.extra_selection_system_prompts = (
                extra_selection_system_prompts
            )
        if len_context is not None:
            FastappSettings.len_context = len_context
