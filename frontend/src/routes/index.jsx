import { createBrowserRouter } from 'react-router-dom';
import Home from '../pages/Home';
import Athletes from '../pages/Athletes';
import Events from '../pages/Events';
import Predictions from '../pages/Predictions';
import MedalCount from '../pages/MedalCount';
import DashboardLayout from '../layouts/DashboardLayout';

const router = createBrowserRouter([
  {
    path: '/',
    element: <DashboardLayout />,
    children: [
      { index: true, element: <Home /> },
      { path: 'athletes', element: <Athletes /> },
      { path: 'events', element: <Events /> },
      { path: 'predictions', element: <Predictions /> },
      { path: 'medal-count', element: <MedalCount /> },
    ],
  },
]);

export default router;