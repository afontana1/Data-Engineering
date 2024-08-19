export interface ApiState {
  isBusy: boolean;
  hasError: boolean;
  errorMessage: string;
}

// Identical to ApiState, but all things are optional.
export interface ApiStateOverride {
  isBusy?: boolean;
  hasError?: boolean;
  errorMessage?: string;
}

export const newApiState = (overrides?: ApiStateOverride): ApiState => {
  const usedOverrides: ApiStateOverride = overrides ? overrides : {};
  return {
    isBusy: false,
    hasError: false,
    errorMessage: "",
    ...usedOverrides,
  };
};
