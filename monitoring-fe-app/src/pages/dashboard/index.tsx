import Header from "../../components/header";
import "./dashboardStyle.scss";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const navigate = useNavigate();

  const cards=()=>{
    return <div className="count-card" onClick={() => {}}>
    <div className="label-style">Total : Device</div>
    <div className="count-text">12</div>
  </div>
  }
  return (
    <div className="dashboard-container">
      <Header />
      <div className="dashboard-body">
        <div className="dashboard-top-count-cards">
          {cards()}
          {cards()}
          {cards()}
          {cards()}
          {cards()}
        </div>

        <div className="dashboard-chart-details">
          <div className="battery-status-card">

          </div>
          <div className="battery-status-card">

          </div>

          <div className="battery-status-card">

          </div>
        </div>
        
      </div>
    </div>
  );
};
export default Dashboard;
