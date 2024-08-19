import React from "react";

export interface ApiButtonProps {
  label: string;
  onClick: any;
  isDisabled?: boolean;
  isLoading?: boolean;
}

export const ApiButton: React.FC<ApiButtonProps> = (props) => {
  const loaderElement = props.isLoading ? (
    <div className="w-7 h-7 flex absolute ">
      <div className="loader" />
    </div>
  ) : null;

  return (
    <div className="w-full mt-4 flex">
      <button
        className="p-3 bg-blue-600 text-white font-semibold rounded-md w-full m-auto 
              disabled:opacity-70"
        type="button"
        onClick={props.onClick}
        disabled={props.isDisabled}
      >
        <div className="flex">
          {loaderElement}
          <div className="h-7 w-full flex">
            <div className="m-auto">{props.label}</div>
          </div>
        </div>
      </button>
    </div>
  );
};
