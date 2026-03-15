import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
// НОВЫЙ ИМПОРТ: Контроллер орбиты
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';


export function loadModel(containerId, modelUrl) {
    const container = document.getElementById(containerId);
    if (!container) return;

    // 1. Сцена
    const scene = new THREE.Scene();
    scene.background = null; // 

    // 2. Камера
    const camera = new THREE.PerspectiveCamera(
        45,
        container.clientWidth / container.clientHeight,
        0.1,
        1000
    );

    // 3. Рендерер
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.outputColorSpace = THREE.SRGBColorSpace; // ВАЖНО для GLTF!

    // --- ВАЖНЫЕ НАСТРОЙКИ ЦВЕТА ---
    // 1. Говорим, что текстуры и свет должны быть конвертированы под монитор
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    // 2. Включаем Tone Mapping (как в кино)
    // ACESFilmic - это стандарт индустрии (Unreal Engine использует его же)
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    // 3. Настраиваем экспозицию (яркость)
    renderer.toneMappingExposure = 1.0;

    container.innerHTML = '';
    container.appendChild(renderer.domElement);
    renderer.domElement.style.position = 'absolute';
    renderer.domElement.style.top = '0';
    renderer.domElement.style.left = '0';
    renderer.domElement.style.width = '100%';
    renderer.domElement.style.height = '100%';
    renderer.domElement.style.zIndex = '10';
    renderer.domElement.style.pointerEvents = 'auto';

    // 4. Контроль (OrbitControls)
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.minDistance = 0.5;
    controls.maxDistance = 20;

    // 5. Окружение (Свет) - вместо старых лампочек
    const pmremGenerator = new THREE.PMREMGenerator(renderer);
    scene.environment = pmremGenerator.fromScene(new RoomEnvironment()).texture;

    // --- 1. Генерируем HTML лоадера программно ---
    const loaderDiv = document.createElement('div');
    loaderDiv.className = 'loader-overlay';
    loaderDiv.innerHTML = `
        <div style="color: #666; font-size: 0.9rem;">Loading...</div>
        <div class="progress-bar">
            <div class="progress-fill"></div>
        </div>
    `;
    container.appendChild(loaderDiv);

    // Находим полоску, чтобы менять её ширину
    const progressFill = loaderDiv.querySelector('.progress-fill');

    // 6. Загрузка модели
    const loader = new GLTFLoader();
    let loadedModel = null;

    loader.load(
        modelUrl,
        // A. ON LOAD (Успех)
        (gltf) => {
            const model = gltf.scene;
            fitCameraToObject(camera, model, controls);
            scene.add(model);

            // Скрываем лоадер
            loaderDiv.style.opacity = '0';
            setTimeout(() => {
                loaderDiv.remove(); // Удаляем из DOM через 0.3 сек
            }, 300);
        },
        // B. ON PROGRESS (Прогресс)
        (xhr) => {
            if (xhr.total > 0) {
                const percent = (xhr.loaded / xhr.total) * 100;
                progressFill.style.width = percent + '%';
            }
        },
        // C. ON ERROR (Ошибка)
        (error) => {
            console.error('Ошибка загрузки:', error);
            loaderDiv.innerHTML = `<div class="error-msg">❌ Ошибка загрузки<br>
                <small>Проверьте файл</small></div>`;
        }
    );

    // 7. Анимация
    function animate() {
        requestAnimationFrame(animate);
        controls.update(); // ОБНОВЛЯЕМ КОНТРОЛЛЕР
        renderer.render(scene, camera);
    }
    animate();

    // Resize handler
    window.addEventListener('resize', () => {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });
}

// Вспомогательная функция центровки (обновленная с controls)
function fitCameraToObject(camera, object, controls) {
    const boundingBox = new THREE.Box3();
    boundingBox.setFromObject(object);

    const center = boundingBox.getCenter(new THREE.Vector3());
    const size = boundingBox.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);

    // Сдвигаем модель в центр
    object.position.x = -center.x;
    object.position.y = -center.y;
    object.position.z = -center.z;

    // Ставим камеру
    const fov = camera.fov * (Math.PI / 180);
    let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2)) * 1.5;

    camera.position.set(cameraZ, cameraZ * 0.5, cameraZ);
    camera.lookAt(0, 0, 0);

    // ВАЖНО: Обновляем цель контроллера, чтобы вращение было вокруг центра модели
    controls.target.set(0, 0, 0);
    controls.update();

    camera.updateProjectionMatrix();
}