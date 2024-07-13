import React from "react";

const Input = React.forwardRef(({ className, ...props }, ref) => {
  return (
    <input
      className={`
        w-full px-3 py-2 text-sm
        border border-gray-300 rounded-md
        focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
        placeholder-gray-400
        ${className}
      `}
      ref={ref}
      {...props}
    />
  );
});

Input.displayName = "Input";

export { Input };
