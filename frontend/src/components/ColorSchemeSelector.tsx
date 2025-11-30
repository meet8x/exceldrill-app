import React, { useEffect, useState } from 'react';
import { client } from '../api/client';
import { Palette, Check } from 'lucide-react';

interface ColorSchemeSelectorProps {
    currentScheme?: string;
    onSchemeChange?: (scheme: string) => void;
}

interface ColorSchemeDetails {
    primary: string;
    secondary: string;
    tertiary: string;
    quaternary: string;
    background: string;
    text: string;
    palette: string[];
}

export const ColorSchemeSelector: React.FC<ColorSchemeSelectorProps> = ({ currentScheme, onSchemeChange }) => {
    const [schemes, setSchemes] = useState<string[]>([]);
    const [details, setDetails] = useState<Record<string, ColorSchemeDetails>>({});
    const [selected, setSelected] = useState<string>(currentScheme || 'kpmg');
    const [isOpen, setIsOpen] = useState(false);

    useEffect(() => {
        fetchSchemes();
    }, []);

    const fetchSchemes = async () => {
        try {
            const response = await client.get('/color-schemes');
            setSchemes(response.data.schemes);
            setDetails(response.data.details);
        } catch (error) {
            console.error("Failed to fetch color schemes", error);
        }
    };

    const handleSelect = async (scheme: string) => {
        setSelected(scheme);
        setIsOpen(false);
        if (onSchemeChange) onSchemeChange(scheme);

        try {
            await client.post('/preferences/color-scheme', { scheme });
        } catch (error) {
            console.error("Failed to save preference", error);
        }
    };

    return (
        <div className="relative">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
                <Palette className="w-4 h-4 text-gray-600" />
                <span className="text-sm font-medium text-gray-700 capitalize">{selected} Theme</span>
            </button>

            {isOpen && (
                <div className="absolute top-full right-0 mt-2 w-64 bg-white rounded-xl shadow-lg border border-gray-100 p-2 z-50 animate-in fade-in zoom-in-95 duration-200">
                    <div className="space-y-1">
                        {schemes.map((scheme) => (
                            <button
                                key={scheme}
                                onClick={() => handleSelect(scheme)}
                                className={`w-full flex items-center justify-between p-2 rounded-lg transition-colors ${selected === scheme ? 'bg-blue-50 text-blue-700' : 'hover:bg-gray-50 text-gray-700'
                                    }`}
                            >
                                <div className="flex items-center gap-3">
                                    <div className="flex -space-x-1">
                                        {details[scheme]?.palette.slice(0, 4).map((color, i) => (
                                            <div
                                                key={i}
                                                className="w-4 h-4 rounded-full border border-white shadow-sm"
                                                style={{ backgroundColor: color }}
                                            />
                                        ))}
                                    </div>
                                    <span className="text-sm font-medium capitalize">{scheme}</span>
                                </div>
                                {selected === scheme && <Check className="w-4 h-4" />}
                            </button>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};
