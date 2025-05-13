from flask import render_template, flash, redirect, url_for, request, current_app, g, abort
from app import db
from app.main import main_bp
from app.main.forms import BookForm, SearchForm
from app.models import Book, User
from app.auth.routes import login_required
from app.utils import save_picture
import os
from sqlalchemy import or_


@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    search_form = SearchForm()
    query = request.args.get('q')
    page = request.args.get('page', 1, type=int)

    if search_form.validate_on_submit():
        query = search_form.query.data
        return redirect(url_for('main.index', q=query))

    if query:
        books_query = g.user.books.filter(
            or_(
                Book.title.ilike(f'%{query}%'),
                Book.author.ilike(f'%{query}%'),
                Book.genre.ilike(f'%{query}%')
            )
        )
        flash(f'Showing search results for "{query}"', 'info')
    else:
        books_query = g.user.books

    books_pagination = books_query.order_by(Book.timestamp.desc()).paginate(
        page=page, per_page=current_app.config.get('BOOKS_PER_PAGE', 5), error_out=False
    )
    books = books_pagination.items

    return render_template('index.html', title='My Favorite Books', books=books,
                           search_form=search_form, pagination=books_pagination, query=query)


@main_bp.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        filename = None
        if form.cover_image.data:
            try:
                filename = save_picture(form.cover_image.data)
                if not filename:
                    flash('Invalid file type or error saving image.', 'warning')
            except Exception as e:
                current_app.logger.error(f"File upload error: {e}")
                flash('An error occurred during file upload.', 'danger')

        new_book = Book(
            title=form.title.data,
            author=form.author.data,
            genre=form.genre.data,
            publication_year=form.publication_year.data,
            description=form.description.data,
            owner=g.user
        )
        if filename:
            new_book.cover_image_filename = filename

        try:
            db.session.add(new_book)
            db.session.commit()
            flash('Your book has been added!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error adding book: {e}")
            flash(f'Error adding book: {str(e)}', 'danger')

    return render_template('manage_book.html', title='Add New Book', form=form, action="Add")


@main_bp.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.owner != g.user:
        abort(403)

    form = BookForm(obj=book)

    current_cover_image = book.cover_image_filename

    if form.validate_on_submit():
        filename = book.cover_image_filename
        if form.cover_image.data and form.cover_image.data.filename != '':
            try:
                if book.cover_image_filename:
                    old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], book.cover_image_filename)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

                filename = save_picture(form.cover_image.data)
                if not filename:
                    flash('Invalid file type or error saving image.', 'warning')
                    return render_template('manage_book.html', title='Edit Book', form=form, book=book, action="Edit",
                                           current_cover_image=current_cover_image)
            except Exception as e:
                current_app.logger.error(f"File upload error during edit: {e}")
                flash('An error occurred during file upload.', 'danger')
                return render_template('manage_book.html', title='Edit Book', form=form, book=book, action="Edit",
                                       current_cover_image=current_cover_image)

        book.title = form.title.data
        book.author = form.author.data
        book.genre = form.genre.data
        book.publication_year = form.publication_year.data
        book.description = form.description.data
        if filename:
            book.cover_image_filename = filename

        try:
            db.session.commit()
            flash('Your book has been updated!', 'success')
            return redirect(url_for('main.view_book', book_id=book.id))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating book: {e}")
            flash(f'Error updating book: {str(e)}', 'danger')

    elif request.method == 'GET':
        form.title.data = book.title
        form.author.data = book.author
        form.genre.data = book.genre
        form.publication_year.data = book.publication_year
        form.description.data = book.description

    return render_template('manage_book.html', title='Edit Book', form=form, book=book, action="Edit",
                           current_cover_image=current_cover_image)


@main_bp.route('/book/<int:book_id>')
@login_required
def view_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.owner != g.user:
        abort(403)
    return render_template('view_book.html', title=book.title, book=book)


@main_bp.route('/delete_book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.owner != g.user:
        abort(403)
    try:
        if book.cover_image_filename:
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], book.cover_image_filename)
            if os.path.exists(image_path):
                os.remove(image_path)

        db.session.delete(book)
        db.session.commit()
        flash('The book has been deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting book: {e}")
        flash(f'Error deleting book: {str(e)}', 'danger')
    return redirect(url_for('main.index'))