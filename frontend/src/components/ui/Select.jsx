import React from "react";

const Select = React.forwardRef(({ className, children, ...props }, ref) => {
  return (
    <select
      className={`
        w-full px-3 py-2
        border border-gray-300 rounded-md
        focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
        bg-black border-black text-white
        appearance-none
        ${className}
      `}
      ref={ref}
      {...props}
    >
      {children}
    </select>
  );
});

Select.displayName = "Select";

export { Select };
