import React, { useState, useEffect } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { Select } from "./ui/Select";
import { Button } from "./ui/Button";

const MedalCountGraph = () => {
  const [sports, setSports] = useState([]);
  const [selectedSport, setSelectedSport] = useState("");
  const [medalData, setMedalData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/sports_by_season")
      .then((response) => response.json())
      .then((data) => {
        const allSports = [...data.Summer, ...data.Winter].sort();
        setSports(allSports);
        setSelectedSport(allSports[0]);
      })
      .catch((error) => setError(error.message));
  }, []);

  const fetchMedalData = () => {
    setLoading(true);
    fetch(`http://localhost:8000/medal_counts/${selectedSport}`)
      .then((response) => response.json())
      .then((data) => {
        setMedalData(data.slice(0, 10)); // Top 10 countries
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message);
        setLoading(false);
      });
  };

  return (
      <div className="w-full">
        <h2 className="text-center">Medal Count by Country</h2>
        <div className="text-xl font-bold p-5"> Select sport:</div>
        <div className="text-black p-5">
          <Select
            value={selectedSport}
            onChange={(e) => setSelectedSport(e.target.value)}
          >
            {sports.map((sport) => (
              <option key={sport} value={sport}>
                {sport}
              </option>
            ))}
          </Select>
          <Button onClick={fetchMedalData} disabled={loading}>
            {loading ? "Loading..." : "Fetch Data"}
          </Button>
        </div>
      {error && <div>{error}</div>}
      <div className="w-auto h-96 p-10">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={medalData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="country" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="gold" name="Gold" fill="#FFD700" />
            <Bar dataKey="silver" name="Silver" fill="#C0C0C0" />
            <Bar dataKey="bronze" name="Bronze" fill="#CD7F32" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default MedalCountGraph;
