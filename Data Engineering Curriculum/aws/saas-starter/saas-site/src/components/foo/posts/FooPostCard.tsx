import * as React from "react";

interface FooPostCardProps {
  title?: string;
  content?: string;
  author?: string;
  isLoading: boolean;
}

const FooPostCard: React.FC<FooPostCardProps> = (props) => {
  let content;

  if (props.isLoading) {
    content = (
      <div className="flex h-12">
        <div className="m-auto">
          <div className="loader-dark"></div>
        </div>
      </div>
    );
  } else {
    content = (
      <>
        <div className="flex justify-between">
          <div className="font-bold">{props.title}</div>
          <div className="text-sm text-blue-600 mb-1">by {props.author}</div>
        </div>
        <div className="text-gray-500">{props.content}</div>
      </>
    );
  }

  return <div className="mb-2 p-2 bg-gray-50 rounded-sm">{content}</div>;
};

export default FooPostCard;
