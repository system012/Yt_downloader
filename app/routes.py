from flask import render_template, request, send_file, redirect, session, flash
from flask_session import Session
import app.forms
from app.forms import DownloadForm
from app.download import link_handler, extract_playlist_urls_and_titles, tar_files, is_playlist

from app import app


@app.route('/', methods=['GET', 'POST'])
def index():
    form = DownloadForm()
    if request.method == "POST":
        link = request.form.get('link')
        session['link'] = link
        if is_playlist(link):
            return redirect('/download')

        return redirect('/single')

    return render_template('index.html', form=form)

@app.route('/download', methods=['GET'])
def download():
    form = DownloadForm()
    link = session['link']
    urls, titles = extract_playlist_urls_and_titles(link)
    session['urls'] = urls

    return render_template('download.html', titles=titles, form=form)

@app.route('/download/<id>', methods=['GET'])
def download_file(id):

    link = session['urls'][int(id)]
    file_to_send, file_name = link_handler(link)
    
    return send_file(file_to_send, attachment_filename=file_name, as_attachment=True)

@app.route('/download/all', methods=['POST'])
def download_all():
    urls = session['urls']
    downloaded_files = []
    for url in urls:
        downloaded_file, _ = link_handler(url)
        downloaded_files.append(downloaded_file)
    
    tar_location = tar_files(downloaded_files)
    
    return send_file(tar_location, attachment_filename='playlist.tar', as_attachment=True)

@app.route('/single', methods=['GET'])
def download_single():
    link = session['link']
    file_to_send, file_name = link_handler(link)

    return send_file(file_to_send, attachment_filename=file_name, as_attachment=True)