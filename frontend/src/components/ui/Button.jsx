import React from "react";

const Button = React.forwardRef(({ className, children, ...props }, ref) => {
  return (
    <button
      className={`
        px-4 py-2 text-sm font-medium text-white
        bg-blue-600 rounded-md
        hover:bg-blue-700
        focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
        ${className}
      `}
      ref={ref}
      {...props}
    >
      {children}
    </button>
  );
});

Button.displayName = "Button";

export { Button };
