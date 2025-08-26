import { Link } from 'react-router-dom';

// Un stil simplu pentru butoanele de navigare
const adminButtonStyles = {
    display: 'block',
    padding: '15px 30px',
    margin: '10px 0',
    backgroundColor: '#646cff',
    color: 'white',
    textDecoration: 'none',
    borderRadius: '8px',
    textAlign: 'center',
    width: '200px'
};

export default function AdminDashboardPage() {
  return (
    <div>
      <h2>Admin Dashboard</h2>
      <p>Selectează o opțiune de mai jos pentru a continua.</p>
      <hr />
      <div>
        <Link to="/admin/categories" style={adminButtonStyles}>
          Gestionează Categorii
        </Link>
        {/* Aici vom adăuga în viitor un buton pentru "Gestionează Produse" */}
      </div>
    </div>
  );
}