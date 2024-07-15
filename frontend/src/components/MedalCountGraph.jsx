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
import { Select } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2 } from "lucide-react";

const MedalCountGraph = () => {
  const [sports, setSports] = useState([]);
  const [selectedSport, setSelectedSport] = useState("");
  const [medalData, setMedalData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/sports/sports_by_season")
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
    <Card className="w-full shadow-lg">
      <CardHeader>
        <CardTitle className="text-2xl font-bold">Medal Count by Country</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col md:flex-row items-center space-y-4 md:space-y-0 md:space-x-4 mb-6">
          <Select
            value={selectedSport}
            onValueChange={setSelectedSport}
            className="w-full md:w-64"
          >
            {sports.map((sport) => (
              <Select.Option key={sport} value={sport}>
                {sport}
              </Select.Option>
            ))}
          </Select>
          <Button
            onClick={fetchMedalData}
            disabled={loading}
            className="w-full md:w-auto"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Loading
              </>
            ) : (
              "Fetch Data"
            )}
          </Button>
        </div>

        {error && (
          <div className="text-red-500 mb-4 p-2 bg-red-100 rounded">
            Error: {error}
          </div>
        )}

        <div className="w-full h-96 bg-white rounded-lg overflow-hidden">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={medalData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
              <XAxis
                dataKey="country"
                tick={{ fill: '#333', fontSize: 12 }}
                tickLine={{ stroke: '#333' }}
              />
              <YAxis
                tick={{ fill: '#333', fontSize: 12 }}
                tickLine={{ stroke: '#333' }}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(255, 255, 255, 0.8)',
                  border: 'none',
                  borderRadius: '4px',
                  boxShadow: '0 2px 5px rgba(0,0,0,0.1)'
                }}
              />
              <Legend
                wrapperStyle={{
                  paddingTop: '20px'
                }}
              />
              <Bar dataKey="gold" name="Gold" fill="#FFD700" radius={[4, 4, 0, 0]} />
              <Bar dataKey="silver" name="Silver" fill="#C0C0C0" radius={[4, 4, 0, 0]} />
              <Bar dataKey="bronze" name="Bronze" fill="#CD7F32" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
};

export default MedalCountGraph;