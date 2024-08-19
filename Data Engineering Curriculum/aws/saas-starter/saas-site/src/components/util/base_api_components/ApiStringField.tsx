import React from "react";

export interface ApiStringFieldProps {
  label: string;
  value: string;
  setValue: React.Dispatch<React.SetStateAction<string>>;
  type: string;
}

type ReactStringHook = [string, React.Dispatch<React.SetStateAction<string>>];

export class ApiStringField {
  private readonly props: ApiStringFieldProps;
  public readonly value: string;

  constructor(props: ApiStringFieldProps) {
    this.props = props;
    this.value = props.value;
  }

  public static fromHook(
    label: string,
    hook: ReactStringHook,
    type: string = "text"
  ) {
    const field = new ApiStringField({
      label,
      value: hook[0],
      setValue: hook[1],
      type,
    });
    return field;
  }

  public static emailFromHook(hook: ReactStringHook) {
    return this.fromHook("Email", hook, "email");
  }

  public static passwordFromHook(hook: ReactStringHook) {
    return this.fromHook("Password", hook, "password");
  }

  public asComponent(isDisabled: boolean) {
    return (
      <div className="w-full">
        <div className="text-sm font-bold mb-1 text-gray-600">
          {this.props.label}
        </div>
        <input
          className="border mb-5 p-2 border-gray-300 rounded-md w-full text-gray-700 
              disabled:opacity-70 disabled:bg-gray-100"
          type={this.props.type}
          name={this.props.type}
          defaultValue={this.props.value.toString()}
          onChange={(e) => this.props.setValue(e.currentTarget.value)}
          disabled={isDisabled}
        />
      </div>
    );
  }
}
