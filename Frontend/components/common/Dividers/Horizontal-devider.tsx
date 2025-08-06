import React from 'react';

interface HorizintalDeviderProps {
  thickness?: string;
  color?: string;
  weight?: string;
  spacing?: string;
}

const HorizintalDevider: React.FC<HorizintalDeviderProps> = ({
  thickness = 'h-[0.1px]',
  color = 'bg-gray-700',
  weight = 'w-[px]',
}) => {
  return <div className={`${thickness} ${weight} ${color}`} />;
};

export default HorizintalDevider;
