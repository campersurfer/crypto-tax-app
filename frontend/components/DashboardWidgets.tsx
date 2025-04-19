import React from "react";

interface WidgetProps {
  title: string;
  value: string | number;
  icon?: React.ReactNode;
  colorClass?: string;
}

const WidgetCard: React.FC<WidgetProps> = ({ title, value, icon, colorClass }) => (
  <div className={`card shadow bg-base-200 ${colorClass || ''} w-48 m-2`}>
    <div className="card-body flex flex-col items-center">
      {icon && <div className="text-3xl mb-2">{icon}</div>}
      <div className="text-lg font-bold">{title}</div>
      <div className="text-2xl mt-1">{value}</div>
    </div>
  </div>
);

export const DashboardWidgets: React.FC = () => {
  // TODO: Replace with real data from backend or props
  const widgets = [
    {
      title: "Top Token",
      value: "ETH",
      icon: <span>🪙</span>,
      colorClass: "border-primary"
    },
    {
      title: "Biggest Trade",
      value: "$12,500",
      icon: <span>💸</span>,
      colorClass: "border-success"
    },
    {
      title: "NFT Activity",
      value: "7 transfers",
      icon: <span>🎨</span>,
      colorClass: "border-accent"
    },
  ];

  return (
    <div className="flex flex-wrap justify-center mb-8">
      {widgets.map((w, idx) => (
        <WidgetCard key={idx} {...w} />
      ))}
    </div>
  );
};
