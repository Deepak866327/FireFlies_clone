import { ReactNode } from "react";

import ComingSoonBadge from "@/components/ComingSoonBadge";
import Card from "@/components/ui/Card";

interface PlaceholderCardProps {
  title: string;
  description?: string;
  icon?: ReactNode;
}

export default function PlaceholderCard({ title, description, icon }: PlaceholderCardProps) {
  return (
    <Card>
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2">
          {icon}
          <h3 className="text-sm font-semibold text-gray-900">{title}</h3>
        </div>
        <ComingSoonBadge />
      </div>
      {description && <p className="mt-2 text-sm text-gray-500">{description}</p>}
    </Card>
  );
}
