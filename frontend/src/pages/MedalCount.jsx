// src/pages/MedalCount.jsx
import React from "react";
import MedalCountGraph from "../components/MedalCountGraph";

export default function MedalCount() {
  return (
    <div>
      <h1 className="righteous-regular text-2xl">Medal Count</h1>
      <MedalCountGraph />
    </div>
  );
}
