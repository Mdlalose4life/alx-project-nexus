import React from 'react';

interface VerticalDividerProps {
  height?: string;
  color?: string;
  thickness?: string;
}

const VerticalDivider: React.FC<VerticalDividerProps> = ({
  height = 'h-[31px]',
  color = 'bg-gray-300',
  thickness = 'w-px',
}) => {
  return <div className={`${height} ${thickness} ${color}`} />;
};

export default VerticalDivider;
