import React, { useState, useRef } from 'react';
import { Upload, Camera, FileText, BarChart3, AlertCircle, CheckCircle, Clock, User, Calendar, Download, Eye, Brain, TrendingUp } from 'lucide-react';

const MedicalAIPlatform = () => {
  const [activeTab, setActiveTab] = useState('upload');
  const [selectedImage, setSelectedImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [analysisHistory, setAnalysisHistory] = useState([
    { id: 1, date: '2025-07-10', result: 'Normal', confidence: 0.95, patient: 'Ahmet K.' },
    { id: 2, date: '2025-07-09', result: 'Pneumonia', confidence: 0.87, patient: 'Ayşe M.' },
    { id: 3, date: '2025-07-08', result: 'Normal', confidence: 0.92, patient: 'Mehmet L.' }
  ]);
  const fileInputRef = useRef(null);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setSelectedImage(e.target.result);
        // Simulated AI analysis
        setTimeout(() => {
          setPrediction({
            result: Math.random() > 0.5 ? 'Normal' : 'Pneumonia',
            confidence: (Math.random() * 0.3 + 0.7).toFixed(2),
            risks: ['Sigara kullanımı', 'Yaş faktörü', 'Aile geçmişi'],
            recommendations: ['Düzenli kontrol', 'Sigarayı bırakın', 'Egzersiz yapın']
          });
        }, 2000);
      };
      reader.readAsDataURL(file);
    }
  };

  const TabButton = ({ id, icon: Icon, label, active }) => (
    <button
      onClick={() => setActiveTab(id)}
      className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
        active ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
      }`}
    >
      <Icon size={20} />
      {label}
    </button>
  );

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                🫁 Akciğer Hastalıkları AI Tespit Platformu
              </h1>
              <p className="text-gray-600">Yapay zeka destekli tıbbi görüntü analizi ve kişiselleştirilmiş raporlama</p>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm text-gray-500">Toplam Analiz</p>
                <p className="text-2xl font-bold text-blue-600">1,247</p>
              </div>
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                <Brain className="text-blue-600" size={24} />
              </div>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <div className="flex gap-2 mb-6 overflow-x-auto">
          <TabButton id="upload" icon={Upload} label="Görüntü Yükle" active={activeTab === 'upload'} />
          <TabButton id="analysis" icon={BarChart3} label="Analiz Sonuçları" active={activeTab === 'analysis'} />
          <TabButton id="history" icon={Clock} label="Geçmiş" active={activeTab === 'history'} />
          <TabButton id="dashboard" icon={TrendingUp} label="Dashboard" active={activeTab === 'dashboard'} />
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Panel */}
          <div className="lg:col-span-2">
            {activeTab === 'upload' && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  <Camera className="text-blue-600" />
                  X-Ray Görüntüsü Yükle
                </h2>
                
                <div 
                  className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer hover:border-blue-400 transition-colors"
                  onClick={() => fileInputRef.current?.click()}
                >
                  {selectedImage ? (
                    <div className="space-y-4">
                      <img 
                        src={selectedImage} 
                        alt="Uploaded X-ray" 
                        className="max-w-full max-h-80 mx-auto rounded-lg shadow-md"
                      />
                      <p className="text-gray-600">Görüntü yüklendi. Analiz için bekleyin...</p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <Upload className="mx-auto text-gray-400" size={48} />
                      <div>
                        <p className="text-lg font-medium text-gray-700">X-Ray görüntüsünü yükleyin</p>
                        <p className="text-gray-500">PNG, JPG, JPEG formatları desteklenir</p>
                      </div>
                    </div>
                  )}
                </div>
                
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleImageUpload}
                  accept="image/*"
                  className="hidden"
                />
              </div>
            )}

            {activeTab === 'analysis' && prediction && (
              <div className="space-y-6">
                {/* AI Analysis Results */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                  <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                    <Brain className="text-purple-600" />
                    AI Analiz Sonuçları
                  </h2>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <div className={`p-4 rounded-lg ${prediction.result === 'Normal' ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
                      <div className="flex items-center gap-2 mb-2">
                        {prediction.result === 'Normal' ? 
                          <CheckCircle className="text-green-600" size={20} /> : 
                          <AlertCircle className="text-red-600" size={20} />
                        }
                        <h3 className="font-medium">Tespit Sonucu</h3>
                      </div>
                      <p className={`text-lg font-semibold ${prediction.result === 'Normal' ? 'text-green-800' : 'text-red-800'}`}>
                        {prediction.result}
                      </p>
                    </div>
                    
                    <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                      <div className="flex items-center gap-2 mb-2">
                        <BarChart3 className="text-blue-600" size={20} />
                        <h3 className="font-medium">Güven Skoru</h3>
                      </div>
                      <p className="text-lg font-semibold text-blue-800">
                        {(prediction.confidence * 100).toFixed(1)}%
                      </p>
                    </div>
                  </div>

                  {/* Risk Factors */}
                  <div className="mb-6">
                    <h3 className="font-medium mb-3">Risk Faktörleri</h3>
                    <div className="flex flex-wrap gap-2">
                      {prediction.risks.map((risk, index) => (
                        <span key={index} className="px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-sm">
                          {risk}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Recommendations */}
                  <div>
                    <h3 className="font-medium mb-3">Öneriler</h3>
                    <ul className="space-y-2">
                      {prediction.recommendations.map((rec, index) => (
                        <li key={index} className="flex items-center gap-2">
                          <CheckCircle className="text-green-600" size={16} />
                          <span className="text-gray-700">{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Explanation */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                  <h3 className="font-medium mb-4 flex items-center gap-2">
                    <Eye className="text-indigo-600" />
                    AI Açıklaması
                  </h3>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <p className="text-gray-700 leading-relaxed">
                      Model, akciğer dokusundaki yoğunluk değişikliklerini, hava yolu açıklığını ve potansiyel anormallikleri analiz ederek bu sonuca ulaştı. 
                      Özellikle alt loblarda gözlenen opasiteler değerlendirildi.
                    </p>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'history' && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  <Clock className="text-gray-600" />
                  Analiz Geçmişi
                </h2>
                
                <div className="space-y-4">
                  {analysisHistory.map((analysis) => (
                    <div key={analysis.id} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                          <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                            <User className="text-blue-600" size={20} />
                          </div>
                          <div>
                            <p className="font-medium">{analysis.patient}</p>
                            <p className="text-sm text-gray-500">{analysis.date}</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-4">
                          <div className={`px-3 py-1 rounded-full text-sm ${
                            analysis.result === 'Normal' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                          }`}>
                            {analysis.result}
                          </div>
                          <div className="text-sm text-gray-500">
                            {(analysis.confidence * 100).toFixed(1)}%
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'dashboard' && (
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-gray-500">Toplam Analiz</p>
                        <p className="text-2xl font-bold text-blue-600">1,247</p>
                      </div>
                      <BarChart3 className="text-blue-600" size={32} />
                    </div>
                  </div>
                  
                  <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-gray-500">Normal Sonuç</p>
                        <p className="text-2xl font-bold text-green-600">892</p>
                      </div>
                      <CheckCircle className="text-green-600" size={32} />
                    </div>
                  </div>
                  
                  <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-gray-500">Anormal Sonuç</p>
                        <p className="text-2xl font-bold text-red-600">355</p>
                      </div>
                      <AlertCircle className="text-red-600" size={32} />
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                  <h3 className="font-medium mb-4">Aylık Analiz Trendi</h3>
                  <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
                    <p className="text-gray-500">Grafik burada görüntülenecek</p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Right Panel */}
          <div className="space-y-6">
            {/* Quick Stats */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="font-medium mb-4">Hızlı İstatistikler</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Bugünkü Analizler</span>
                  <span className="font-semibold">23</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Ortalama Güven</span>
                  <span className="font-semibold">91.2%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Aktif Kullanıcılar</span>
                  <span className="font-semibold">156</span>
                </div>
              </div>
            </div>

            {/* Recent Activity */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="font-medium mb-4">Son Aktiviteler</h3>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                    <CheckCircle className="text-green-600" size={16} />
                  </div>
                  <div>
                    <p className="text-sm font-medium">Normal sonuç</p>
                    <p className="text-xs text-gray-500">2 dakika önce</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center">
                    <AlertCircle className="text-red-600" size={16} />
                  </div>
                  <div>
                    <p className="text-sm font-medium">Anormal tespit</p>
                    <p className="text-xs text-gray-500">5 dakika önce</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <Upload className="text-blue-600" size={16} />
                  </div>
                  <div>
                    <p className="text-sm font-medium">Yeni görüntü yüklendi</p>
                    <p className="text-xs text-gray-500">8 dakika önce</p>
                  </div>
                </div>
              </div>
            </div>

            {/* System Status */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="font-medium mb-4">Sistem Durumu</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">AI Model</span>
                  <span className="text-green-600 font-medium">Aktif</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Sunucu</span>
                  <span className="text-green-600 font-medium">Çevrimiçi</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Veritabanı</span>
                  <span className="text-green-600 font-medium">Bağlı</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MedicalAIPlatform;